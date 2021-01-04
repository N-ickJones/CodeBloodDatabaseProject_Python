"""
This is ran periodically to update items on site with the database
"""

from core_app.Periodic.graph import Graph


def update_homepage_graph():
    graph = Graph()
    graph.drop_table()
    graph.create_table()
    graph.fill_table()
    if graph.check_table():
        graph.get_donations()
        graph.build_graph()
        graph.build_bar_graph()
    else:
        print('Donations Table Does Not Exist')


update_homepage_graph()


"""
medical_staff_entries = (
            
            (('"id"', '1'),
            ('"start_date"', ''),
            ('"job"', 'doctor'),
            ('"level"', ''),
            ('"is_active"', ''),
            ('"rating"', ''),
            ('"vacation_days"', ''),
            ('"on_vacation"', '')),

            (('"id"', '2'),
             ('"start_date"', ''),
             ('"job"', 'nurse'),
             ('"level"', ''),
             ('"is_active"', ''),
             ('"rating"', ''),
             ('"vacation_days"', ''),
             ('"on_vacation"', '')),

            (('"id"', '3'),
             ('"start_date"', ''),
             ('"job"', 'janitor'),
             ('"level"', ''),
             ('"is_active"', ''),
             ('"rating"', ''),
             ('"vacation_days"', ''),
             ('"on_vacation"', '')),

            (('"id"', '4'),
             ('"start_date"', ''),
             ('"job"', 'surgeon'),
             ('"level"', ''),
             ('"is_active"', ''),
             ('"rating"', ''),
             ('"vacation_days"', ''),
             ('"on_vacation"', '')),

            (('"id"', '5'),
             ('"start_date"', ''),
             ('"job"', 'doctor'),
             ('"level"', ''),
             ('"is_active"', ''),
             ('"rating"', ''),
             ('"vacation_days"', ''),
             ('"on_vacation"', '')),

        )
"""
