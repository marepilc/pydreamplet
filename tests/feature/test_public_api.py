import pydreamplet as dp
from pydreamplet import colors, core, scales, shapes


def test_all_exports_are_public_attributes():
    for name in dp.__all__:
        assert hasattr(dp, name), name


def test_animation_classes_are_exported_from_top_level():
    assert dp.Animate is core.Animate
    assert dp.AnimateTransform is core.AnimateTransform


def test_scale_classes_are_exported_from_top_level():
    assert dp.map is scales.map
    assert dp.LinearScale is scales.LinearScale
    assert dp.BandScale is scales.BandScale
    assert dp.PointScale is scales.PointScale
    assert dp.OrdinalScale is scales.OrdinalScale
    assert dp.ColorScale is scales.ColorScale
    assert dp.SquareScale is scales.SquareScale
    assert dp.CircleScale is scales.CircleScale


def test_shape_helpers_are_exported_from_top_level():
    assert dp.star is shapes.star
    assert dp.linear_path is shapes.linear_path
    assert dp.step_path is shapes.step_path
    assert dp.catmull_rom_path is shapes.catmull_rom_path
    assert dp.basis_spline is shapes.basis_spline
    assert dp.monotone_x_path is shapes.monotone_x_path
    assert dp.monotone_y_path is shapes.monotone_y_path
    assert dp.cardinal_spline is shapes.cardinal_spline
    assert dp.polygon is shapes.polygon
    assert dp.superellipse is shapes.superellipse
    assert dp.rounded_polygon is shapes.rounded_polygon
    assert dp.blob is shapes.blob
    assert dp.cross is shapes.cross
    assert dp.arc is shapes.arc
    assert dp.ring is shapes.ring


def test_color_helpers_are_exported_from_top_level():
    assert dp.Color is colors.Color
    assert dp.Theme is colors.Theme
    assert dp.blend_colors is colors.blend_colors
    assert dp.hex_to_rgb is colors.hex_to_rgb
    assert dp.rgb_to_hex is colors.rgb_to_hex
    assert dp.color2rgba is colors.color2rgba
    assert dp.blend is colors.blend
    assert dp.random_color is colors.random_color
    assert dp.generate_colors is colors.generate_colors
    assert dp.tone is colors.tone
