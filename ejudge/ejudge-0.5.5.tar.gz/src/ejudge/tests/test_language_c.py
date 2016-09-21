from ejudge import functions
from ejudge.tests import abstract as base

sources = """
## ok
#include<stdio.h>

int main(void) {
    char buffer[100];
    printf("name: ");
    scanf("%s", buffer);
    printf("hello %s!\n", buffer);
}


## wrong
#include<stdio.h>

int main(void) {
    char buffer[100];
    puts("name: ");
    scanf("%s", buffer);
    printf("%s\n", buffer);
}


## syntax
a b

## error
int main(void) {
    char buffer[10];
    char c = buffer[1000];
}


## recursive
int f(int x):
    return (x <= 1)? 1: x * f(x - 1);

int main(void) {
    printf("%d\n", f(5));
}


## twoinputs
#include<stdio.h>
void main() {
    char name[100], job[200];
    printf("name: ");
    scanf("%s", name);
    printf("job: ");
    scanf("%s", job);
    printf("%s, %s\n", name, job);
}
"""


class TesCSupport(base.TestLanguageSupport):
    base_lang = 'c'
    source_all = sources

    def test_c_program_with_two_inputs(self):
        src = self.get_source('twoinputs')
        result = functions.run(src, ['foo', 'bar'], lang='c', sandbox=False)
        case = result[0]
        result.pprint()
        assert list(case) == ['name: ', 'foo', 'job: ', 'bar', 'foo, bar']
