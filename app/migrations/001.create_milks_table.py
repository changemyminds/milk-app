from yoyo import step

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS public.milks (
            id           SERIAL  NOT NULL,
            time_range   VARCHAR(256) NOT NULL,
            cc           INTEGER NOT NULL,
            create_time  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CONSTRAINT milks_pkey PRIMARY KEY (id)
        );
        """,
        "DROP TABLE IF EXISTS public.milks;"),
]
