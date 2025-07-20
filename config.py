import os

STORAGE_DIR = "storage"  # directory to cache the generated index
DATA_DIR = "data"  # directory containing the documents to index
MODEL_DIR = "localmodels"  # directory containing the model files, use None if use remote model
CONFIG_STORE_FILE = "config_store.json" # local storage for configurations

# The device that used for running the model. 
# Set it to 'auto' will automatically detect (with warnings), or it can be manually set to one of 'cuda', 'mps', 'cpu', or 'xpu'.
LLM_DEVICE = "auto"
EMBEDDING_DEVICE = "auto"

HISTORY_LEN = 3

MAX_TOKENS = 4096

TEMPERATURE = 0.5

TOP_K = 5

SYSTEM_PROMPT = "You are an AI assistant that helps users to find accurate information. You can answer questions, provide explanations, and generate text based on the input. Please answer the user's question exactly in the same language as the question or follow user's instructions. For example, if user's question is in Chinese, please generate answer in Chinese as well. If you don't know the answer, please reply the user that you don't know. If you need more information, you can ask the user for clarification. Please be professional to the user."

RESPONSE_MODE = [
            "compact",
            "refine",
            "tree_summarize",
            "simple_summarize",

]
DEFAULT_RESPONSE_MODE = "simple_summarize"

OLLAMA_API_URL = "http://localhost:11434"

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

LLM_API_LIST = {
    # Ollama API
    "Ollama": {
        "api_base": OLLAMA_API_URL,
        "models": [],
        "provider": "Ollama",
    },
    # OpenAI API
    "OpenAI": {
        "api_key": OPENAI_API_KEY,
        "api_base": "https://api.openai.com/v1/",
        "models": ["gpt-4", "gpt-3.5", "gpt-4o"],
        "provider": "OpenAI",
    },
    # ZhiPu API
    "Zhipu": {
        "api_key": ZHIPU_API_KEY,
        "api_base": "https://open.bigmodel.cn/api/paas/v4/",
        "models": ["glm-4-plus", "glm-4-0520", "glm-4", "glm-4-air", "glm-4-airx", "glm-4-long", "glm-4-flashx", "glm-4-flash", "glm-4v-plus", "glm-4v"],
        "provider": "Zhipu",
    },
    # Moonshot API
    "Moonshot": {
        "api_key": MOONSHOT_API_KEY,
        "api_base": "https://api.moonshot.cn/v1/",
        "models": ["moonshot-v1-8k","moonshot-v1-32k","moonshot-v1-128k"],
        "provider": "Moonshot",
    },
    # DeepSeek API
    "DeepSeek": {
        "api_key": DEEPSEEK_API_KEY,
        "api_base": "https://api.deepseek.com/v1/",
        "models": ["deepseek-chat"],
        "provider": "DeepSeek",
    },
}

DEFAULT_CHUNK_SIZE = 4096
DEFAULT_CHUNK_OVERLAP = 1024
ZH_TITLE_ENHANCE = False

MONGO_URI = "mongodb://localhost:27017"
REDIS_URI = "redis://localhost:6379"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
ES_URI = "http://localhost:9200"

DEFAULT_VS_TYPE = "es"

DEFAULT_CHAT_STORE = "redis"
CHAT_STORE_FILE_NAME = "chat_store.json"
CHAT_STORE_KEY = "user1"

HF_ENDPOINT = "https://hf-mirror.com"

DEFAULT_EMBEDDING_MODEL = "bge-small-zh-v1.5"
EMBEDDING_MODEL_PATH = {
    "bge-small-zh-v1.5": "BAAI/bge-small-zh-v1.5",
    "bge-large-zh-v1.5": "BAAI/bge-large-zh-v1.5",
}

DEFAULT_RERANKER_MODEL = "bge-reranker-base"
RERANKER_MODEL_PATH = {
    "bge-reranker-base": "BAAI/bge-reranker-base",
    "bge-reranker-large": "BAAI/bge-reranker-large",
}

USE_RERANKER = False
RERANKER_MODEL_TOP_N = 2
RERANKER_MAX_LENGTH = 1024

THINKRAG_ENV = os.getenv("THINKRAG_ENV", "development")
DEV_MODE = THINKRAG_ENV == "development"

DEFAULT_INDEX_NAME = "knowledge_base"