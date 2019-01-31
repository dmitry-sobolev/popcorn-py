
ломается my_declarative_base.metadata.create_all(engine)

File "/Users/irinabystrova/PycharmProjects/popcorn-py/models.py", line 20, in create_series_table
    my_declarative_base.metadata.create_all(engine)

File "/Users/irinabystrova/.local/share/virtualenvs/popcorn-py-HdSeT82j/lib/python3.7/site-packages/sqlalchemy/sql/schema.py", line 4200, in create_all bind._run_visitor(

AttributeError: 'SeriesPipeline' object has no attribute '_run_visitor'