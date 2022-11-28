"""
Unit test: test src/models.py
"""
def test_new_unlabeled_data(unlabeled_data):
    """
    GIVEN UnlabeledData
    WHEN a new unlabeled data point is created
    THEN check the columns are defined correctly
    """
    assert unlabeled_data.raw_text_input == 'Foo bar'
    assert unlabeled_data.model_output == 'Foo bar'
