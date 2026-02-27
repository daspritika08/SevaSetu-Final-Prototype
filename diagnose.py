"""Diagnose AWS and Bedrock connectivity issues"""

import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()

print("="*70)
print("SEVASETU DIAGNOSTIC TOOL")
print("="*70)

# Step 1: Check .env file
print("\n1. Checking .env configuration...")
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')
kb_id = os.getenv('KNOWLEDGE_BASE_ID')

print(f"   AWS_ACCESS_KEY_ID: {access_key[:10] if access_key else 'NOT SET'}...")
print(f"   AWS_SECRET_ACCESS_KEY: {'SET' if secret_key else 'NOT SET'}")
print(f"   AWS_REGION: {region}")
print(f"   KNOWLEDGE_BASE_ID: {kb_id}")

if not all([access_key, secret_key, region, kb_id]):
    print("   ❌ Missing configuration in .env file!")
    exit(1)
print("   ✅ Configuration loaded")

# Step 2: Test AWS credentials
print("\n2. Testing AWS credentials...")
try:
    sts = boto3.client('sts', region_name=region)
    identity = sts.get_caller_identity()
    print(f"   ✅ Credentials VALID")
    print(f"   Account: {identity['Account']}")
    print(f"   User ARN: {identity['Arn']}")
except ClientError as e:
    print(f"   ❌ Credentials INVALID: {e}")
    print("\n   Fix: Create new access keys in IAM Console")
    exit(1)

# Step 3: Check Bedrock availability in region
print(f"\n3. Checking Bedrock availability in {region}...")
try:
    bedrock = boto3.client('bedrock', region_name=region)
    models = bedrock.list_foundation_models()
    print(f"   ✅ Bedrock available in {region}")
    print(f"   Available models: {len(models.get('modelSummaries', []))}")
except ClientError as e:
    print(f"   ❌ Bedrock not available: {e}")
    print(f"\n   Note: Bedrock may not be available in {region}")
    print("   Available regions: us-east-1, us-west-2, eu-central-1, ap-northeast-1")

# Step 4: Test Bedrock Agent Runtime
print("\n4. Testing Bedrock Agent Runtime access...")
try:
    bedrock_agent = boto3.client('bedrock-agent-runtime', region_name=region)
    print(f"   ✅ Bedrock Agent Runtime client created")
except Exception as e:
    print(f"   ❌ Failed to create client: {e}")
    exit(1)

# Step 5: Test Knowledge Base access
print(f"\n5. Testing Knowledge Base access (ID: {kb_id})...")
model_arn = os.getenv('MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-2-lite-v1:0')
print(f"   Using model: {model_arn}")
try:
    response = bedrock_agent.retrieve_and_generate(
        input={'text': 'test'},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kb_id,
                'modelArn': model_arn
            }
        }
    )
    print(f"   ✅ Knowledge Base accessible!")
    print(f"   Test query successful")
except ClientError as e:
    error_code = e.response['Error']['Code']
    error_msg = e.response['Error']['Message']
    print(f"   ❌ Knowledge Base error [{error_code}]: {error_msg}")
    
    if error_code == 'ResourceNotFoundException':
        print(f"\n   Fix: Check Knowledge Base ID is correct")
        print(f"   Current ID: {kb_id}")
    elif error_code == 'UnrecognizedClientException':
        print(f"\n   Fix: IAM user needs Bedrock permissions")
        print("   Required permissions:")
        print("   - bedrock:InvokeModel")
        print("   - bedrock:Retrieve")
        print("   - bedrock:RetrieveAndGenerate")
    elif error_code == 'AccessDeniedException':
        print(f"\n   Fix: Add Bedrock permissions to IAM user")
    exit(1)

print("\n" + "="*70)
print("✅ ALL CHECKS PASSED - Your setup is working!")
print("="*70)
print("\nYou can now run: streamlit run app.py")
