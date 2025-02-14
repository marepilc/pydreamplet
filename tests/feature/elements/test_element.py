import pydreamplet as dp


def test_element_remove_attribute():
    circle = dp.Circle(id="circle")
    assert "id" in str(circle)
    circle.id = None
    assert "id" not in str(circle)

    circle.cx = 10
    assert 'cx="10"' in str(circle)
    circle.attrs({"cx": None})
    assert "cx" not in str(circle)
