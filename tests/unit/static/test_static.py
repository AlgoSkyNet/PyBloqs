from pybloqs.static import Resource, JScript, Css, DependencyTracker, register_interactive, write_interactive
import pytest
from six import StringIO
from mock import patch


def test_resource_local_path():
    name = 'dummy'
    ext = 'ext'
    resource = Resource(name, ext)
    path = resource._local_path
    assert path.endswith(name + ext)


def test_jscript_raises_with_no_name_and_string():
    with pytest.raises(ValueError):
        JScript()


def test_jscript_write_string():
    script = 'test script'
    jscript = JScript(script_string=script, encode=False)
    output = jscript.write()
    output_string = output.__str__()
    assert output_string.startswith('<script>')
    assert output_string.endswith('</script>')
    assert script in output_string

    # Check that output is compressed if we ask for it
    jscript = JScript(script_string=script, encode=True)
    output = jscript.write()
    output_string = output.__str__()
    assert output_string.startswith('<script>')
    assert output_string.endswith('</script>')
    assert 'RawDeflate' in output_string
    assert script not in output_string


def test_jscript_write_string_compressed():
    script = 'test script'
    jscript = JScript(script_string=script)
    stream = StringIO()
    jscript.write_compressed(stream, script)
    output = stream.getvalue()
    assert output.startswith('blocksEval')
    assert script not in output

    # Do not compress if disabled globally
    JScript.global_encode = False
    jscript = JScript(script_string=script, encode=False)
    stream = StringIO()
    jscript.write_compressed(stream, script)
    output = stream.getvalue()
    assert output == script


def test_jscript_load_name():
    with patch('pybloqs.static.Resource.__init__') as constructor:
        JScript(name='some_name')
    constructor.assert_called_once_with('some_name', '.js')


def test_css_raises_with_no_name_and_string():
    with pytest.raises(ValueError):
        Css()


def test_css_write_string():
    css_string = 'test styles'
    css = Css(css_string=css_string)
    output = css.write()
    output_string = output.__str__()
    assert output_string.startswith('<style type="text/css"')
    assert output_string.endswith('</style>')
    assert css_string in output_string


def test_css_load_name():
    with patch('pybloqs.static.Resource.__init__') as constructor:
        Css(name='some_name')
    constructor.assert_called_once_with('some_name', '.css')


def test_css_tag_id():
    css_string = 'test styles'
    tag_id = 'some_tag'
    css = Css(css_string=css_string, tag_id=tag_id)
    output = css.write()
    output_string = output.__str__()
    assert output_string.startswith('<style ')
    assert 'type="text/css"' in output_string
    assert 'id="{}"'.format(tag_id) in output_string
    assert output_string.endswith('</style>')
    assert css_string in output_string


def test_dependency_tracker_retrieve_resources():
    dep = DependencyTracker('res1', 'res2', 'res1')
    assert set(dep) == {'res1', 'res2'}


def test_dependency_tracker_add_resources():
    dep = DependencyTracker()
    dep.add('res1', 'res2', 'res1')
    assert set(dep) == {'res1', 'res2'}


def test_register_interactive_write_interactive():
    register_interactive('test1', 'test2')
    write_interactive()
