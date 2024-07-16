from openai import OpenAI
import os
import re
import json
from datetime import datetime


class LLM:
    def __init__(self,file_path:str = '../task_list.json' ,model_type:str = "deepseek"):
        self.file_path = file_path
        self.model_type = model_type
        self.res = ''
        if self.model_type=='deepseek':
            self.base_url = os.getenv("BASE_URL")
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
        

    def run(self,question:str,language:str = '中文',question_type:str = "question"):
        if question_type == "question":
            prompt:str = '''
                    您是一名地理分析师，您的任务是分析给定的历史或新闻情报，定位事件的内容，发生的位置，时间，相关的人物和历史事件，然后给出事件的地理描述，作为事件的属性信息。
                你要生成的内容要包裹在```event```中，案例格式如下，要包含以下字段，：：
                ```event
                "event_title": "有关ABC公司新产品的情报",
                "event_type": "市场情报",
                "event_content": "根据对社交媒体平台的监听和分析，我们发现了以下有关ABC公司新产品的情报：1. ABC公司将在本月底发布其新的智能手机，该手机将具有更快的处理器、更大的内存和更长的电池寿命。2. 该新产品将是ABC公司在智能手机市场上的重要攻势，旨在与竞争对手的旗舰产品竞争。3. 在社交媒体上，用户对该新产品的期待度较高，有些用户甚至表示愿意预订该产品。",
                "keys": ["Twitter", "Facebook", "LinkedIn"],
                "event_location": "中国北京",
                ```
            生成的内容是一个json格式 用大括号json格式扩住,并将将生成的情报信息包裹在```task```中，要求使用中文、完整且精炼的语言进行描述。
            好的，请根据以下用户输入的问题进行分析生成回答,严格{language}输出：
                {question}
            '''.format(question = question,language = language)

        elif question_type == "message":
            prompt :str = """
            您是一名情报分析官，您的任务是从社交媒体中搜集、分析和归纳情报与线索，并且生成分析报告。请根据以下用户输入，确定任务名称、任务类型、任务内容、技术栈和任务状态，并且将其生成为一个任务信息。
            情报名称应该是一个简短的、能够清晰描述任务的名称，例如“社交媒体情报分析”。
            情报类型应该是一个描述任务性质的词语或短语，例如“情报分析”。
            情报内容应该是一个详细的、能够清晰描述情报来源，时间，地点，事件的文本，例如“根据用户提供的社交媒体账号或关键词，进行情报与线索的搜集、分析和归纳，并且生成分析报告。分析过程需要包括但不限于：1. 确定搜集范围，并且使用相应的工具或方法进行情报搜集；2. 对搜集到的情报进行初步筛选和分类，并且进行深入分析，找出其中的关键信息和线索；3. 对分析结果进行总结和归纳，并且生成分析报告。”。
            关键词应该是一个包含了任务所需要的技术、工具或方法的列表，例如["社交媒体监听工具", "情报分析工具", "数据可视化工具"]。
            你要生成的内容要包裹在```task```中，案例格式如下，要包含以下字段，：
            
            "intelligence_name": "有关ABC公司新产品的情报",
            "intelligence_type": "市场情报",
            "intelligence_content": "根据对社交媒体平台的监听和分析，我们发现了以下有关ABC公司新产品的情报：1. ABC公司将在本月底发布其新的智能手机，该手机将具有更快的处理器、更大的内存和更长的电池寿命。2. 该新产品将是ABC公司在智能手机市场上的重要攻势，旨在与竞争对手的旗舰产品竞争。3. 在社交媒体上，用户对该新产品的期待度较高，有些用户甚至表示愿意预订该产品。",
            "keys": ["Twitter", "Facebook", "LinkedIn"],

            生成的内容是一个json格式 用大括号json格式扩住,并将将生成的情报信息包裹在```task```中，要求使用中文、完整且精炼的语言进行描述。

            好的，请根据以下用户输入的问题进行分析生成回答,严格{language}输出：
            {question}
        """.format(question = question,language = language)

        if self.model_type == "deepseek":
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "您是一名CSDN技术博主，您的任务是从分析用户需求，定位问题并生成具体解决方案。"},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            task = LLM.parse_task(response.choices[0].message.content)
            
        self.save_task(task) # 保存任务
        return task

    @staticmethod
    def parse_task(content): # 从模型生成中字符串匹配提取生成的代码
        pattern = r'```task(.*?)```'  # 使用非贪婪匹配
        match = re.search(pattern, content, re.DOTALL)
        task = match.group(1) if match else content
        task = json.loads(task,strict=False)  # 转换为json格式
        return task

    def save_task(self, task):
        task['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r',encoding='utf-8') as file:
                tasks = json.load(file,strict=False)
            tasks.append(task)
        else:
            tasks = [task]
        with open(self.file_path, 'w',encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False)

