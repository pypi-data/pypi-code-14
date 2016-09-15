# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from alembic import context
from sqlalchemy import create_engine, pool

from murano.db import cfapi_models as models


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
murano_config = config.murano_config

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = models.Base.metadata


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = create_engine(
        murano_config.database.connection,
        poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
