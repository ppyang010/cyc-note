tool基类只有
名称,描述,参数json格式,执行方法,。`schema()` 把前三样拼成 OpenAI function calling 要的格式，
一个工具只有上面这些

发给模型，模型据此决定要不要调、怎么填参数。
没有派生工具
都是从tool 下的直接子类

edit_file
使用 old_string/new_string
使用旧字符串替换新字符串的方式,并且要求旧字符串只出现一次
0次->没