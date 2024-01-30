from pathlib import Path
import os
import shutil
import subprocess
import sys


PICKUP_CONFIG = 'pickup_config'
DEFAULT_CONFIG_NAME = 'MSIAfterburner'
DEFAULT_FOLDER = 'default_backup_MSIAfterburner'
LATEST_BACKUP_FOLDER = 'new_backup_MSIAfterburner'
MAIN_FOLDER = 'replace_config'
PROTILE  ='Profiles'


class Replacer:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.config_file_name = None
        self.dict_config = dict()
        self.selected_config: int = None
        self.PROFILE_PATH = Path(Path.cwd()).joinpath(PROTILE)


    def show_menu(self):
        col_question =  '1. Create backup\n2. Choose config'
        print(col_question)
        while True:
            try:
                choose = input('Type 1 or 2: \n').lower()
                if (choose in ['1', '2']):
                    self.selected_config = int(choose)
                    break
                else:
                    print('Invalid value')
            except KeyboardInterrupt:
                print('Invalid')


    def backup_info(self):
        """Backup is create two folder:
           1. Backup of the first configuration. The first config is stored in the replace_config/default_backup_MSIAfterburner folder 
           and is updated only once at the first start. 
           The second, third, and subsequent ones will not update it. But if you create a backup after replacing the configs, 
           then the config that you currently have in the folder will be saved here. 
           This is done in order not to force you to create folders and backup files.
           2. The most recent backup of your configuration. Saves the last configuration you use in one instance, 
           on the folder new_backup_MSIAfterburner"""
        print(self.backup_info.__doc__)
        

    def create_copy_config(self):
        while True:
            create_copy = input('create copy of your config? yes or no\n ').lower()
            if (create_copy in 'yes'):
                """ Default config """
                path = Path(self.current_dir, Path(MAIN_FOLDER).joinpath(DEFAULT_FOLDER))
                template_file = Path(path).joinpath(f'{DEFAULT_CONFIG_NAME}_copy.cfg')
                is_move_config = Path.exists(path)
                is_file_exist = Path.is_file(template_file)
                get_config_from_cwd = Path(self.PROFILE_PATH, f'{DEFAULT_CONFIG_NAME}.cfg')
                if not is_move_config and not is_file_exist:
                    """ Create folder """
                    self.make_path(self.current_dir, Path(MAIN_FOLDER).joinpath(DEFAULT_FOLDER))
                    """ move file """
                    print(f'copy default backup file with name: {DEFAULT_CONFIG_NAME}.cfg from {self.PROFILE_PATH} to {path}')
                    shutil.copy(get_config_from_cwd, path)
                
                """ Latest backup """
                """ New occurence config """
                second_path = Path(self.current_dir, Path(MAIN_FOLDER).joinpath(LATEST_BACKUP_FOLDER, f'{DEFAULT_CONFIG_NAME}_copy.cfg'))
                self.make_path(self.current_dir, Path(MAIN_FOLDER).joinpath(LATEST_BACKUP_FOLDER))
                print(f'copy default backup file with name:{DEFAULT_CONFIG_NAME}.cfg from {self.PROFILE_PATH} to {second_path}')
                shutil.copy(get_config_from_cwd, second_path)
                break

            elif create_copy == 'no':
                break
        

    def make_path(self, current_dir, fold):
        path_dir = Path(current_dir, fold)
        is_exist = Path.exists(path_dir)
        if not is_exist:
            self.create_folder(path_dir, fold)


    def create_folder(self, path, name):
        try:
            Path.mkdir(path, parents=True, exist_ok=False)
            print(f'root file {name} is creating...')
        except FileExistsError:
            pass


    def check_if_exist_cfg_files(self):
        path = Path(self.current_dir).joinpath(MAIN_FOLDER, PICKUP_CONFIG)
        files = list(path.glob('*.cfg'))
        is_search = True
        if len(files) > 0: is_search = False
        while is_search:
            print(f'Put your config to direcory replace_config/pickup_config. When you put press yes\n')
            is_put = input('').lower()
            if (is_put == 'yes'):
                files = list(path.glob('*.cfg'))
                if len(files) > 0: break
                print('files with extension .cfg not found\n')
            else:
                print('Uncorrect input')

            
    def if_backup(self):
        if (self.selected_config == 1):
            self.backup_info()
            self.choose_backup()

    
    def choose_backup(self):
        self.create_copy_config()


    def replace_cfg(self):
        self.show_config()
        self.choose_config()
        self.copy_config()


    def show_config(self):
        path = Path(self.current_dir).joinpath(MAIN_FOLDER, PICKUP_CONFIG)
        entries = os.listdir(path)
        all_entries = list(map(str, entries))
        filter_by_ext = list(filter(lambda x: x.endswith('.cfg'), all_entries))
        if len(filter_by_ext) != 0:
            enum_value = list(enumerate(filter_by_ext))
            for k in enum_value:
                print(f'num: {k[0]}  config: {k[1]}')
                self.dict_config.update({k[0]: k[1]})  
        else:
            print('files with ext cfg not found')

    
    def choose_config(self):
        while True:
            try:
                choose = int(input('\nChoose config by key - number \n'))
                if choose in self.dict_config.keys():
                    self.config_file_name = self.dict_config[choose]
                    break
                else:
                    print('Incorrect number')
            except ValueError as err:
                print(f' is not a number')


    def copy_config(self):
        pick_cfg = Path(self.current_dir).joinpath(MAIN_FOLDER, PICKUP_CONFIG, self.config_file_name)
        """ current_dir = Path(self.PROFILE_PATH).joinpath(f'{DEFAULT_CONFIG_NAME}.cfg') """
        path_to_remove = Path(self.PROFILE_PATH).joinpath(f'{DEFAULT_CONFIG_NAME}.cfg')
        print('remove main config: MSIAfterburner.cfg')
        try:
            Path.unlink(path_to_remove)
        except FileNotFoundError:
            print(f'file {path_to_remove} not found')
            sys.exit()
        print(f'move {self.config_file_name} to dir {self.PROFILE_PATH}')
        """ or use only shutil.copy without renaming and delete """
        shutil.copy(pick_cfg, self.PROFILE_PATH)
        path_to_rename = Path(self.PROFILE_PATH, self.config_file_name)
        print(f'rename {self.config_file_name} to {DEFAULT_CONFIG_NAME}.cfg')

        path_to_rename.rename(Path(self.PROFILE_PATH).joinpath(f'{DEFAULT_CONFIG_NAME}.cfg'))
        print('file renamed')


    def run_afterburner(self):
        subprocess.run(f'{DEFAULT_CONFIG_NAME}.exe', shell=True)
        input('dsds')
        

    def root(self):
        """ Create root folder """
        self.make_path(self.current_dir, MAIN_FOLDER)

        """ Create folder for config """
        make_pickup_path = Path(self.current_dir).joinpath(MAIN_FOLDER)
        self.make_path(make_pickup_path, PICKUP_CONFIG)
        self.check_if_exist_cfg_files()

        """ Create backup """
        """ Choose branch """
        self.show_menu()
        self.if_backup()
        self.replace_cfg()

        """ run proccess """
        self.run_afterburner()

    
replace_cfg = Replacer()
replace_cfg.root()