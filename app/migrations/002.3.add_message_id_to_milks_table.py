from yoyo import step, group

group([
    step(
        """
        ALTER TABLE public.milks
        ADD COLUMN line_message_id INTEGER;
        """,
        "ALTER TABLE public.milks DROP COLUMN line_message_id;"
    ),
    step(
        """
        ALTER TABLE public.milks
        ADD CONSTRAINT milks_line_message_id_fkey FOREIGN KEY (line_message_id)
        REFERENCES public.line_messages (id);
        """,
        "ALTER TABLE public.milks DROP CONSTRAINT milks_line_message_id_fkey;"
    )
])
