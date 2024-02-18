from yoyo import step


steps = [
    step(
        """
        ALTER TABLE public.milks
        ALTER COLUMN create_time TYPE timestamp with time zone;
        """,
        """
        ALTER TABLE public.milks
        ALTER COLUMN create_time TYPE timestamp without time zone;
        """
    )
]
