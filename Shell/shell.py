from File_Systems.file_system import FileSystem
from File_Systems.exceptions import Exceptions

class Shell:
    def __init__(self):
        self.file_system = None

    def run_shell(self):
        
        while (1):
            try:
                user_input = input()
                user_input = user_input.strip().split()
                if len(user_input) == 0:
                    print()
                elif len(user_input) == 1:
                    if user_input[0].lower() == "dr" and self.file_system != None:
                        self.file_system.directory()
                    elif user_input[0].lower() == "in":
                        self.file_system = FileSystem()
                    ################    DEBUG   ##################
                    elif user_input[0].lower() == "q":
                        break
                    ##############################################
                    else:
                        print("error")
                elif len(user_input) == 2:
                    try:
                        num = int(user_input[1])
                    except ValueError:
                        name = str(user_input[1])

                    if user_input[0].lower() == "cr" and self.file_system != None:
                        self.file_system.create(name)
                    elif user_input[0].lower() == "de" and self.file_system != None:
                        self.file_system.destroy(name)
                    elif user_input[0].lower() == "op" and self.file_system != None:
                        self.file_system.open(name)
                    elif user_input[0].lower() == "cl" and self.file_system != None:
                        self.file_system.close(num)
                    else:
                        print("error")
                elif len(user_input) == 3:
                    try:
                        mem = int(user_input[1])
                        count = int(user_input[2])
                    except ValueError:
                        mem = int(user_input[1])
                        string = str(user_input[2])

                    if user_input[0].lower() == "rm" and self.file_system != None:
                        self.file_system.read_memeory(mem, count)
                    elif user_input[0].lower() == "wm" and self.file_system != None:
                        mem = int(user_input[1])
                        string = str(user_input[2])
                        self.file_system.write_memory(mem, string)
                    elif user_input[0].lower() == "sk" and self.file_system != None:
                        self.file_system.seek(mem,count)
                    else:
                        print("error")

                elif len(user_input) == 4:
                    try:
                        index = int(user_input[1])
                        mem = int(user_input[2])
                        count = int(user_input[3])
                    except ValueError:
                        print("error")
                    
                    if user_input[0].lower() == "rd" and self.file_system != None:
                        self.file_system.read(index, mem, count)
                    elif user_input[0].lower() == "wr" and self.file_system != None:
                        self.file_system.write(index, mem, count)
                    else:
                        print("error")

                else:
                    print("error")
            except EOFError:
                break

if __name__ == "__main__":
    s = Shell()
    s.run_shell()