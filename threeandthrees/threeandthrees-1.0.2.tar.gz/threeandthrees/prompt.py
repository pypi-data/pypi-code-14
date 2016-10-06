import cmd
import words
from colorama import init, Fore
init(autoreset=True)


class ThreesWords(cmd.Cmd):

    prompt = Fore.GREEN + ">  "
    intro = "Welcome to the 3&3s game!  Try 'help' (no 's)"

    def do_count(self, arg):
        "Get the number of answers for a three letter core"
        matches = words.monger.answer_count(arg)
        if matches is None:
            ct = 0
        else:
            ct = matches

        print("{0} has {1} matches in American english".format(
            arg, ct
        ))

    def do_check(self, arg):
        "Test a word"
        result = words.monger.check(arg)
        if result is True:
            print("{0} works!".format(arg))
        else:
            print("{0} doesn't work :(".format(arg))

    def do_generate(self, arg):
        "Get a three letter core"
        core = words.monger.generate()
        print("Your core is {0}.".format(core))

    def do_answers(self, arg):
        "Get the answers for a three letter core"
        matches = words.monger.answers(arg)
        if matches is None:
            print(
                "{0} has no answers in American english".format(arg, matches)
            )
        else:
            print("{0} has these answers: {1}".format(arg, matches))

    def do_challenge(self, arg):
        "Challenge me!"
        words.monger.formulate_challenge()
        words.monger.show_challenge()

    def do_claim(self, arg):
        "Claim to solve a word in the active challenge"
        result = words.monger.claim(arg)
        if result:
            words.monger.show_challenge()
        else:
            print("Nope :(")

    def do_show(self, arg):
        "Show the active challenge"
        words.monger.show_challenge()

    def do_exit(self, line):
        "Exit"
        return True

    def do_quit(self, line):
        "Exit"
        return True

    def do_EOF(self, line):
        return True

    def do_help(self, line):
        "Instructions on all commands"
        print("""
Challenge commands:
    challenge : take a challenge
    claim <nine letters> : assert an answer in the challenge
    show : show the challenge

Cheating commands:
    check <nine letters> : check if that is a word
    count <three letters> : number of answers for a three letter sequence
    answers <three letters> : get the answers for a three letter sequence

Challenge commands:
    help : show this
    exit : exit
    quit : exit


        """)


def main():
    ThreesWords().cmdloop()


if __name__ == '__main__':
    main()
