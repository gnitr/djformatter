djformatter
===========

Reformat Django Template Files

This is a lightweight and simplistic python script used to reformat Django Template files.

### What it does

It reindents each line according to the block of code (Javascript, HTML, Django Template) it belongs. The newly formatted file is sent to the standard output.

Note that this tool will not change the line the instructions are on. It will only change the indentation of each line.

### Motivation

I developed this tool when I had to maintain extremely messy and almost unreadable templates inherited from other developers

### Limitations

* The code parsing is very simplistic and therefore the block detection mechanism can easily be fooled
* Currently it won't deal well with:
  * non valid HTML
  * special HTML elements such as comments or doctype
  * non valid Django
  * non valid Javascript
  * so this script is supposed to be run on working templates producing no error and valid HTML

## Example

This command

```
$> python srcode.py format test\samples\demo.html
```

returns

```
{% block myblock %}
    {% if result_set %}
        <script>
            $(function(){
                var a = [1,2,3];
                var b = 'demo ';
                for (i in a) {
                    b += a[i];
                }
            });
        </script>
        <div class="cl1">
            <ul>
                {% for item in result_set %}
                    <li>
                        {{ item.label }}
                    </li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}
{% endblock %}
```
