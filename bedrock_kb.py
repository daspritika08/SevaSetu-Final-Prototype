"""
Bedrock Knowledge Base Query Module

This module provides functionality to query AWS Bedrock Knowledge Base
for government scheme information using the retrieve_and_generate API.
"""

import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Knowledge Base Configuration (loaded from environment variables)
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID', 'OUQVSP38X2')
MODEL_ARN = os.getenv('MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2')


class BedrockKnowledgeBase:
    """Client for interacting with AWS Bedrock Knowledge Base"""
    
    def __init__(self, region_name=None, aws_access_key_id=None, aws_secret_access_key=None):
        """
        Initialize Bedrock Agent Runtime client
        
        Args:
            region_name (str): AWS region name (default: from environment or us-east-1)
            aws_access_key_id (str): AWS access key ID (default: from environment)
            aws_secret_access_key (str): AWS secret access key (default: from environment)
        """
        if region_name is None:
            region_name = os.getenv('AWS_REGION', 'us-east-1')
        
        if aws_access_key_id is None:
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        
        if aws_secret_access_key is None:
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        try:
            self.client = boto3.client(
                'bedrock-agent-runtime',
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
            logger.info(f"Bedrock client initialized for region: {region_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    def query_knowledge_base(self, user_prompt, max_tokens=512, temperature=0.7):
        """
        Query the Knowledge Base using retrieve_and_generate
        
        Args:
            user_prompt (str): User's question or query
            max_tokens (int): Maximum tokens in response (default: 512)
            temperature (float): Model temperature for response generation (default: 0.7)
        
        Returns:
            dict: Response containing generated text, citations, and metadata
                {
                    'text': str,
                    'citations': list,
                    'session_id': str
                }
        
        Raises:
            ClientError: If the API call fails
            ValueError: If user_prompt is empty
        """
        if not user_prompt or not user_prompt.strip():
            raise ValueError("user_prompt cannot be empty")
        
        try:
            logger.info(f"Querying Knowledge Base with prompt: {user_prompt[:100]}...")
            
            response = self.client.retrieve_and_generate(
                input={
                    'text': user_prompt
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                        'modelArn': MODEL_ARN
                    }
                }
            )
            
            # Extract response data
            output_text = response.get('output', {}).get('text', '')
            citations = response.get('citations', [])
            session_id = response.get('sessionId', '')
            
            logger.info(f"Query successful. Response length: {len(output_text)} chars")
            logger.info(f"Citations found: {len(citations)}")
            
            return {
                'text': output_text,
                'citations': citations,
                'session_id': session_id
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"Bedrock API error [{error_code}]: {error_message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error querying Knowledge Base: {e}")
            raise


def query_knowledge_base(user_prompt):
    """
    Convenience function to query the Knowledge Base
    
    Args:
        user_prompt (str): User's question or query
    
    Returns:
        dict: Response containing generated text, citations, and metadata
    """
    kb = BedrockKnowledgeBase()
    return kb.query_knowledge_base(user_prompt)


# Example usage
if __name__ == "__main__":
    # Example query
    prompt = "What government schemes are available for farmers in India?"
    
    try:
        result = query_knowledge_base(prompt)
        
        print("\n" + "="*80)
        print("QUERY RESULT")
        print("="*80)
        print(f"\nPrompt: {prompt}")
        print(f"\nResponse:\n{result['text']}")
        print(f"\nSession ID: {result['session_id']}")
        print(f"\nNumber of Citations: {len(result['citations'])}")
        
        if result['citations']:
            print("\nCitations:")
            for i, citation in enumerate(result['citations'], 1):
                print(f"\n  [{i}] Retrieved References:")
                for ref in citation.get('retrievedReferences', []):
                    print(f"      - Location: {ref.get('location', {}).get('s3Location', {}).get('uri', 'N/A')}")
                    print(f"        Content: {ref.get('content', {}).get('text', '')[:200]}...")
        
    except Exception as e:
        print(f"Error: {e}")
