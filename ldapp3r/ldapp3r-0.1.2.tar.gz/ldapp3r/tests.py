from ldap3 import Server, Connection
server = Server('ldaps://ldap1.ludd.ltu.se', get_info='*', use_ssl=True)
conn = Connection(server)
conn.bind()

from ldapper import LdapperInterface as Ldapper

User = Ldapper.define("ou=people,dc=ludd,dc=ltu,dc=se", "uid=%s")
User.wrap = True
me = User.using(conn).get("armedguy")

print(me._entry)
me.loginShell = "/usr/local/bin/bash"
User.using(conn).save(me)
