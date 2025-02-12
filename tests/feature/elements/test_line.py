import pydreamplet as dp


def test_line_length():
    line = dp.Line(0, 0, 10, 0)
    assert line.length == 10
    line = dp.Line(0, 0, 10, 10)
    assert line.length == 14.142135623730951
    line = dp.Line(0, 0, 0, 10)
    assert line.length == 10
    line = dp.Line(0, 0, -10, 0)
    assert line.length == 10
    line = dp.Line(0, 0, -10, -10)
    assert line.length == 14.142135623730951
    line = dp.Line(0, 0, 0, -10)
    assert line.length == 10
    line = dp.Line(0, 0, 10, -10)
    assert line.length == 14.142135623730951
    line = dp.Line(0, 0, -10, 10)
    assert line.length == 14.142135623730951
    line = dp.Line(0, 0, 10, 10)
    assert line.length == 14.142135623730951
    line = dp.Line(0, 0, 0, 0)
    assert line.length == 0
    line = dp.Line(0, 0, 0, 1)
    assert line.length == 1
    line = dp.Line(0, 0, 1, 0)
    assert line.length == 1
    line = dp.Line(0, 0, 1, 1)
    assert line.length == 1.4142135623730951
    line = dp.Line(0, 0, 1, -1)
    assert line.length == 1.4142135623730951
    line = dp.Line(0, 0, -1, 1)
    assert line.length == 1.4142135623730951
    line = dp.Line(0, 0, -1, -1)
    assert line.length == 1.4142135623730951
    line = dp.Line(0, 0, -1, 0)
    assert line.length == 1
    line = dp.Line(0, 0, 0, -1)
    assert line.length == 1


def test_line_attrs():
    line = dp.Line(0, 0, 10, 0)
    assert line.x1 == 0
    assert line.y1 == 0
    assert line.x2 == 10
    assert line.y2 == 0
    line.attrs({"x1": 1, "y1": 2, "x2": 3, "y2": 4})
    assert line.x1 == 1
    assert line.y1 == 2
    assert line.x2 == 3
    assert line.y2 == 4


def test_line_angle():
    line = dp.Line(0, 0, 10, 0)
    assert line.angle == 0
    line = dp.Line(0, 0, 10, 10)
    assert line.angle == 45
    line = dp.Line(0, 0, 0, 10)
    assert line.angle == 90
    line = dp.Line(0, 0, -10, 10)
    assert line.angle == 135
    line = dp.Line(0, 0, -10, 0)
    assert line.angle == 180
    line = dp.Line(0, 0, -10, -10)
    assert line.angle == 225
    line = dp.Line(0, 0, 0, -10)
    assert line.angle == 270
    line = dp.Line(0, 0, 10, -10)
    assert line.angle == 315
    line = dp.Line(0, 0, 10, 10)
    assert line.angle == 45
    line = dp.Line(0, 0, 0, 0)
    assert line.angle == 0
    line = dp.Line(0, 0, 0, 1)
    assert line.angle == 90
    line = dp.Line(0, 0, 1, 0)
    assert line.angle == 0
    line = dp.Line(0, 0, 1, 1)
    assert line.angle == 45
    line = dp.Line(0, 0, 1, -1)
    assert line.angle == 315
    line = dp.Line(0, 0, -1, 1)
    assert line.angle == 135
    line = dp.Line(0, 0, -1, -1)
    assert line.angle == 225
    line = dp.Line(0, 0, -1, 0)
    assert line.angle == 180
    line = dp.Line(0, 0, 0, -1)
    assert line.angle == 270
    line = dp.Line(0, 0, -1, 1)
    assert line.angle == 135
    line = dp.Line(0, 0, 1, 1)
    assert line.angle == 45
