---
#这是一些不常用但是逼格较高的模块，或许会有使用需求。

synchronize  复制海量小文件场景使用,以及打包解包用途。

lineinfile   修改文件内容使用  regexp=^ENV_KEY=

get_url      

vault        加密模块

wait_for     任务的暂停

---
#提高效率的一些逻辑

register     注册变量

debug

changed_when

when         与register结合使用功能强大

gather_facts

environment

changed_when    changed_fail  ---------- in, not in,exists ...

ignore_errors   

delegate_to   指定在特定主机运行

local_action  指定为本地任务

tags          标签   
	ansible-playbook test.yml --tags "TAG_NAME"
	ansible-playbook test.yml --skip-tags "TAG_NAME"

block         块功能适用于多个任务共用同一套任务参数情况,还可以用来处理任务异常。--- (rescue,always)

include       引用其他YAML文件

set_fact      设置fact变量

lookup 


#善用jinja2模板


#插件开发     filter，callback




