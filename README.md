自用nastool，目前配合阿里云盘使用，所以更新都是为了更方便的使用这套流程：

目前媒体入库方案：阿里云盘手动搜索资源，存放到阿里云盘特定目录下，借助nastool的目录同步功能，实现刮削metadata，目录迁移。

已调整功能如下：
+ 增加大语言模型 优化重命名逻辑：阿里云盘的资源，命名不规范，所以借助 大语言模型 如 llama3-70b 格式化文件名，从而大大提升识别精度。
  + 使用方式，配置三个系统环境变量，推荐使用 [openrouter](https://openrouter.ai/models):
      - OPENAI_API_KEY=sk-or-v1-xxxx
      - OPENAI_API_BASE=https://openrouter.ai/api/v1        
      - OPENAI_API_MODEL=meta-llama/llama-3-70b-instruct
      - ![image](https://github.com/escapeWu/nas-tools/assets/159442095/1a39028f-ed3e-4b7a-9b1e-c507186a05c3)


代办：
+ 大语言模型的相关变量，从环境变量，集成到webUI进行配置

