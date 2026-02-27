"""
Configuration Loader for SevaSetu Application

This module loads configuration from environment variables and .env file.
It provides a centralized configuration management system.
"""

import os
from pathlib import Path
from typing import Optional
import logging

# Try to import python-dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv not installed. Install with: pip install python-dotenv")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config:
    """Configuration class for SevaSetu application"""
    
    def __init__(self):
        """Initialize configuration by loading from .env file and environment variables"""
        self._load_env_file()
        self._load_config()
    
    def _load_env_file(self):
        """Load environment variables from .env file if it exists"""
        if DOTENV_AVAILABLE:
            env_path = Path('.env')
            if env_path.exists():
                load_dotenv(env_path)
                logger.info("Loaded configuration from .env file")
            else:
                logger.warning(".env file not found. Using environment variables only.")
        else:
            logger.warning("python-dotenv not available. Using environment variables only.")
    
    def _load_config(self):
        """Load all configuration values from environment variables"""
        
        # AWS Configuration
        self.aws_region = self._get_env('AWS_REGION', 'us-east-1')
        self.aws_access_key_id = self._get_env('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = self._get_env('AWS_SECRET_ACCESS_KEY')
        
        # Bedrock Knowledge Base Configuration
        self.knowledge_base_id = self._get_env('KNOWLEDGE_BASE_ID', 'OUQVSP38X2')
        self.model_arn = self._get_env(
            'MODEL_ARN',
            'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2'
        )
        
        # Model Configuration
        self.max_tokens = int(self._get_env('MAX_TOKENS', '512'))
        self.temperature = float(self._get_env('TEMPERATURE', '0.7'))
        self.top_p = float(self._get_env('TOP_P', '0.9'))
        
        # S3 Configuration
        self.s3_bucket_name = self._get_env('S3_BUCKET_NAME', '')
        self.s3_data_prefix = self._get_env('S3_DATA_PREFIX', 'schemes/')
        
        # Application Configuration
        self.app_title = self._get_env('APP_TITLE', 'SevaSetu - Government Schemes Assistant')
        self.app_icon = self._get_env('APP_ICON', '🌾')
        self.log_level = self._get_env('LOG_LEVEL', 'INFO')
        
        # Session Configuration
        self.session_timeout_minutes = int(self._get_env('SESSION_TIMEOUT_MINUTES', '30'))
        
        # Supported Languages
        languages_str = self._get_env('SUPPORTED_LANGUAGES', 'hindi,odia,tamil,telugu,bengali')
        self.supported_languages = [lang.strip() for lang in languages_str.split(',')]
        
        # Validate critical configuration
        self._validate_config()
    
    def _get_env(self, key: str, default: Optional[str] = None) -> str:
        """
        Get environment variable with optional default value
        
        Args:
            key (str): Environment variable name
            default (str, optional): Default value if not found
        
        Returns:
            str: Environment variable value or default
        """
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"Environment variable {key} not set and no default provided")
        return value
    
    def _validate_config(self):
        """Validate critical configuration values"""
        errors = []
        
        if not self.knowledge_base_id:
            errors.append("KNOWLEDGE_BASE_ID is required")
        
        if not self.model_arn:
            errors.append("MODEL_ARN is required")
        
        if self.max_tokens <= 0:
            errors.append("MAX_TOKENS must be positive")
        
        if not 0 <= self.temperature <= 1:
            errors.append("TEMPERATURE must be between 0 and 1")
        
        if not 0 <= self.top_p <= 1:
            errors.append("TOP_P must be between 0 and 1")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("Configuration validation passed")
    
    def get_aws_credentials(self) -> dict:
        """
        Get AWS credentials as a dictionary
        
        Returns:
            dict: AWS credentials (may be empty if using IAM roles)
        """
        credentials = {}
        if self.aws_access_key_id:
            credentials['aws_access_key_id'] = self.aws_access_key_id
        if self.aws_secret_access_key:
            credentials['aws_secret_access_key'] = self.aws_secret_access_key
        return credentials
    
    def get_bedrock_config(self) -> dict:
        """
        Get Bedrock configuration as a dictionary
        
        Returns:
            dict: Bedrock configuration
        """
        return {
            'knowledge_base_id': self.knowledge_base_id,
            'model_arn': self.model_arn,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'top_p': self.top_p
        }
    
    def __repr__(self) -> str:
        """String representation of configuration (without sensitive data)"""
        return (
            f"Config(\n"
            f"  aws_region={self.aws_region},\n"
            f"  knowledge_base_id={self.knowledge_base_id},\n"
            f"  model_arn={self.model_arn},\n"
            f"  max_tokens={self.max_tokens},\n"
            f"  temperature={self.temperature},\n"
            f"  top_p={self.top_p},\n"
            f"  app_title={self.app_title},\n"
            f"  supported_languages={self.supported_languages}\n"
            f")"
        )


# Global configuration instance
_config = None


def get_config() -> Config:
    """
    Get the global configuration instance (singleton pattern)
    
    Returns:
        Config: Global configuration instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config():
    """Reload configuration from environment variables"""
    global _config
    _config = Config()
    logger.info("Configuration reloaded")


# Example usage and testing
if __name__ == "__main__":
    print("Loading SevaSetu Configuration...\n")
    
    try:
        config = get_config()
        print(config)
        print("\n" + "="*80)
        print("Configuration loaded successfully!")
        print("="*80)
        
        print("\nAWS Configuration:")
        print(f"  Region: {config.aws_region}")
        print(f"  Credentials configured: {bool(config.get_aws_credentials())}")
        
        print("\nBedrock Configuration:")
        bedrock_config = config.get_bedrock_config()
        for key, value in bedrock_config.items():
            print(f"  {key}: {value}")
        
        print("\nApplication Configuration:")
        print(f"  Title: {config.app_title}")
        print(f"  Icon: {config.app_icon}")
        print(f"  Log Level: {config.log_level}")
        print(f"  Supported Languages: {', '.join(config.supported_languages)}")
        
    except Exception as e:
        print(f"\n❌ Error loading configuration: {e}")
        print("\nPlease ensure:")
        print("  1. Copy .env.template to .env")
        print("  2. Fill in your AWS credentials and configuration")
        print("  3. Install python-dotenv: pip install python-dotenv")
