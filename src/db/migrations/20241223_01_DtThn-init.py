"""init."""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table account
            (
                id   bigserial primary key,
                name text not null unique
            );
        """,
        """
            drop table account;
        """,
    ),
]
