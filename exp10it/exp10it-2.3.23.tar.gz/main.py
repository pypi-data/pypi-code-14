from exp10it import *
import os
import warnings
output=CLIOutput()
warnings.filterwarnings('ignore', '.*have a default value.*',)
scan_way_init()
database_init()
# 要先database_init才有config文件
import config
while 1:
    target = get_one_target_from_db(config.db_name, config.first_targets_table_name)
    if target == None:
        target = get_one_target_from_db(config.db_name, config.targets_table_name)
    if target != None:
        output.good_print("get a target for scan from database:")

        from colorama import init,Fore
        init(autoreset=True)
        output.good_print(Fore.BLUE+target)

        auto_attack(target)
    else:
        output.good_print("all targets scan finished")
        break
