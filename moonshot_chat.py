import os
from langchain_community.chat_models.moonshot import MoonshotChat


os.environ["MOONSHOT_API_KEY"] = "sk-smlULyCmMfg3tdpms8bvT1u1tvu4YYymW9jg0mV2XQoV15pw"
moonshot_chat = MoonshotChat(model="moonshot-v1-32k",max_tokens=16000)
