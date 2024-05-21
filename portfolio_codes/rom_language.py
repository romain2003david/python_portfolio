def print_error(error, line_nb, info=0):

    if info:

        print("{} at line {} [{}]".format(errors_dict[error], line_nb, info))

    else:

        print("{} at line {}".format(errors_dict[error], line_nb))


class Holder:

    def __init__(self, content=0):

        self.string_dict = {}

        self.number_dict = {}

        self.list_dict = {}

        if content != 0:  # a string might be given

            content.split(",")

            for x in content:

                error = Holder.append_thing(x[1], x[0])

                if error and error[:5] == "error":

                    return error

    def append_thing(self, thing, thing_name):

        if len(thing) > 1:

            if (thing[0][0] == "[") and (thing[-1][-1] == "]"):  # it's a list

                list_content = []

                for index in range(len(thing)):

                    if index == 0:

                        list_content.append(thing[index][1:])

                    elif index == len(thing)-1:

                        list_content.append(thing[index][:-1])

                    else:

                        list_content.append(thing[index])

                Holder.append_list(self, Liste(list_content), thing_name)

        else:

            thing = thing[0]

            thing_type = get_thing_type(thing)

            if thing_type[:5] == "error":

                return thing_type

            elif thing_type == "str":

                Holder.append_string(self, thing, thing_name)

            elif thing_type == "int":

                Holder.append_number(self, thing, thing_name)

    def append_string(self, to_append, thing_name):

        self.string_dict[thing_name] = to_append[1:-1]

    def append_number(self, to_append, thing_name):

        self.number_dict[thing_name] = int(to_append)

    def append_list(self, to_append, thing_name):

        self.list_dict[thing_name] = to_append

    def print_content(self):

        print("\nHOLDER\n")

        print("String vars:")

        print(self.string_dict, "\n")

        print("Number vars:")

        print(self.number_dict, "\n")

        print("List vars:")

        for x in self.list_dict:

            print(x, end=" : ")

            self.list_dict[x].print_content()


class Liste:

    def __init__(self, content=0, content_is_list=0):

        self.content = []

        if content != 0:  # a string might be given

            if content_is_list == 0:

                content.split(",")

                for x in content:

                    self.content.append(x)

            else:

                self.content = content

    def print_content(self):

        print(*self.content)


def get_thing_type(thing):

    if thing[0] == "\"":  # string type

        return "str"

    elif thing[0] == "[":  # list type

        return "list"

    else:  # int type

        try:

            int(thing)

            return "int"

        except ValueError:

            return "error2"

            
def decode_affectation(line, holder, line_nb):

    if line[1] == "=":

        # finding type of affected thing

        error = holder.append_thing(line[2:], line[0])

        if error and error[:5] == "error":

            print_error(int(error[5:]), line_nb, str(line[2])+", "+str(line[0]))

    else:

        print_error(3, line_nb)


def print_vars(line, holder):

    holder.print_content()


def decode_line(line, holder, line_nb):

    line[-1] = line[-1][:-1]  # strips the ; or :

    if line [-1] == "":  # gets rid of the semi colon place, which is now useless

        del line[-1]

    if line[0] in dico_line_type.keys():

        dico_line_type[line[0]](line, holder)

    else:  # affectation de variable

        decode_affectation(line, holder, line_nb)


def decode_bloc(bloc, holder, line_nb):

    minus_line = -len(bloc)  # to count lines

    for line in bloc:

        minus_line += 1

        decode_line(line, holder, line_nb+minus_line)


def main():

    # in case file doesn't exist

    file = open("rom_file.txt", "a")

    file.close()

    # reading content

    content = []

    file = open("rom_file.txt", "r")

    for line in file:

        content.append(line)

    file.close()

    ##

    # setting objects that contain variables defined by code

    holder = Holder()

    ##

    bloc = []

    line_nb = 0

    for line in content:

        line_nb += 1

        if line != "\n":  # ignores empty lines

            line = line.split()

            last_car = line[-1][-1]

            bloc.append(line)

            if last_car == ";":

                decode_bloc(bloc, holder, line_nb)

                bloc = []

            elif last_car != ":":  # checks if indentation ":" have been specified, if yes we just keep checking next lines, else syntax error

                print_error(1, line_nb)

                return



if __name__ == "__main__":

    dico_line_type = {"print_vars":print_vars}

    errors_dict = {1:"Syntax Error : missing end line on line {}\n",
                   2:"Unknown type",
                   3:"bad syntax : equal sign should be 2 place"
                   }

    main()
