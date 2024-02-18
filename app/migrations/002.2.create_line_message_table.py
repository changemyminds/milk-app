from yoyo import step

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS public.line_messages (
            id             SERIAL        NOT NULL,
            message_id     VARCHAR(64)   NOT NULL,
            text           VARCHAR(256),
            type           VARCHAR(32)   NOT NULL,
            group_id       VARCHAR(64)   NOT NULL,
            user_id        VARCHAR(64)   NOT NULL,
            timestamp      TIMESTAMPTZ   NOT NULL,
            CONSTRAINT line_messages_pkey PRIMARY KEY (id)
        );
        CREATE INDEX IF NOT EXISTS idx_line_messages_message_id ON public.line_messages (message_id);
        """,
        "DROP TABLE IF EXISTS public.line_messages;"
    ),
]
