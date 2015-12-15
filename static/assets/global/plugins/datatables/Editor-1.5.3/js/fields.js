(function ($, DataTable) {
    if (!DataTable.ext.editorFields) {
        DataTable.ext.editorFields = {};
    }

    var Editor = DataTable.Editor;
    var _fieldTypes = DataTable.ext.editorFields;

    _fieldTypes.mtext = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;

            // Create the elements to use for the input
            conf._input = $(
                    '<div>' +
                    '<input type="text" name="' + conf.name + '"/>' +
                    '</div>')[0];

            // Use the fact that we are called in the Editor instance's scope to call
            // the API method for setting the value when needed
            $('button.inputButton', conf._input).click(function () {
                if (conf._enabled) {
                    that.set(conf.name, $(this).attr('value'));
                }

                return false;
            });

            return conf._input;
        },

        get: function (conf) {
            return $('input', conf._input).attr('value');
        },

        set: function (conf, val) {
            $('input', conf._input).attr('value', val);
        },

        enable: function (conf) {
            conf._enabled = true;
            $('input',conf._input).attr('disabled',false);
        },

        disable: function (conf) {
            conf._enabled = false;
            $('input',conf._input).attr('disabled',true);
        }
    };

    _fieldTypes.mselect = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;

            // Create the elements to use for the input
            var $select = $('<select name="' + conf.name + '"></select>')
            for (var index in conf.options) {
                $select.append('<option value="' + conf.options[index].value + '">' + conf.options[index].label + '</option>')
            }
            $select.addClass('form-control select2me')
            $div = $("<div/>")
            $div.append($select)
            conf._input = $div[0]

            $select.select2({
                placeholder: "Select a State",
                allowClear: true
            });

            // Use the fact that we are called in the Editor instance's scope to call
            // the API method for setting the value when needed

            return conf._input;
        },

        get: function (conf) {
            return $('select', conf._input).attr('value');
        },

        set: function (conf, val) {
            $('select', conf._input).attr('value', val);
        },

        enable: function (conf) {
            conf._enabled = true;
            $('select',conf._input).attr('disabled',false);
        },

        disable: function (conf) {
            conf._enabled = false;
            $("select",conf._input).attr('disabled',true);
        }
    };

    _fieldTypes.mmselect = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;

            // Create the elements to use for the input
            var $select = $('<select name="' + conf.name + '" multiple="multiple"></select')
            for (var index in conf.options) {
                $select.append('<option value="' + conf.options[index].value + '">' + conf.options[index].label + '</option>')
            }
            $select.addClass('form-control select2me')
            $div = $("<div/>")
            $div.append($select)
            conf._input = $div[0]

            $select.select2({
                placeholder: "Select a State",
                allowClear: true
            });

            // Use the fact that we are called in the Editor instance's scope to call
            // the API method for setting the value when needed

            return conf._input;
        },

        get: function (conf) {
            value = $('select', conf._input).select2("val")
            return value
        },

        set: function (conf, val) {
            $('select', conf._input).select2('val', val);
        },

        enable: function (conf) {
            conf._enabled = true;
            $('select',conf._input).attr('disabled',false);
        },

        disable: function (conf) {
            conf._enabled = true;
            $('select',conf._input).attr('disabled',true);
        }
    };

    _fieldTypes.mradio = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;

            // Create the elements to use for the input

            var $div = $("<div/>")
            var $radio_list = $('<div/>')
            $div.append($radio_list)
            for (var index in conf.options) {
                $radio_list.append($(
                        '<label class="radio-inline">' +
                        '<input type="radio" name="' + conf.name + '" id="id_' + conf.name + index + '" value="' + conf.options[index].value + '"/>' +
                        conf.options[index].label +
                        '</label>'
                ))
            }

            $("input", $radio_list).click(function (event) {
                if (conf._enabled) {
                    $('input[checked]', $radio_list).removeAttr('checked');
                    $(this).attr("checked", true)
                }

                return true;
            })
            conf._input = $div[0]

            // Use the fact that we are called in the Editor instance's scope to call
            // the API method for setting the value when needed

            return conf._input;
        },

        get: function (conf) {
            return $('input[checked]', conf._input).attr('value');
        },

        set: function (conf, val) {
            if(val===''){
               val = false
            }
            $('input[value=' + val + ']', conf._input).attr('checked', true);
        },

        enable: function (conf) {
            conf._enabled = true;
            $('input',conf._input).attr('disabled',false);
        },

        disable: function (conf) {
            conf._enabled = false;
            $('input',conf._input).attr('disabled',true);
        }
    };

    _fieldTypes.treeselect = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;


            var $div = $('<div></div>')
            var $portlet = $(
'                <div class="scroller portlet blue-hoki box green">'+
'                    <div class="portlet-title">'+
'                        <div class="caption">'+
'                            <input type="text" id="display" readonly="true">' +
'                        </div>'+
'                        <div class="tools">'+
'                            <a href="javascript:;" class="expand">'+
'                            </a>'+
'                        </div>'+
'                    </div>'+
'                    <div class="portlet-body display-hide">'+
'                        <div id="foreign_key_tree_1" class="tree-demo">'+
'                        </div>'+
'                    </div>'+
'                </div>'
            )
           $portlet.find("#foreign_key_tree_1").jstree({
                "core" : {
                    "themes" : {
                        "responsive": false
                    },
                    // so that create works
                    "check_callback" : true,
                    'data': conf.items
                },
                "types" : {
                    "default" : {
                        "icon" : "fa fa-folder icon-state-warning icon-lg"
                    },
                    "file" : {
                        "icon" : "fa fa-file icon-state-warning icon-lg"
                    }
                },
                "state" : { "key" : "demo2" },
                "plugins" : [ "contextmenu", "dnd", "state", "types" ]
            }).on('select_node.jstree', function(e,data) {
               $portlet.find("#display").val(data.node.text)
            })
            $div.append($portlet)
            conf._input = $div[0]

            // Use the fact that we are called in the Editor instance's scope to call
            // the API method for setting the value when needed

            return conf._input;
        },

        get: function (conf) {
            var $jstree = $("#foreign_key_tree_1",conf._input),
            result =  $jstree.jstree("get_selected")

            if (result.length>0){
                return result[0]
            } else {
                return ''
            }
        },

        set: function (conf, val) {
            var $jstree = $("#foreign_key_tree_1",conf._input)
            setTimeout(function(){
                $('#display',conf._input).val('')
                $jstree.jstree("deselect_all")
                $jstree.jstree("select_node",val)
            },500)
        },

        enable: function (conf) {
            conf._enabled = true;
            $(conf._input).removeClass('disabled');
        },

        disable: function (conf) {
            conf._enabled = false;
            $(conf._input).addClass('disabled');
        }
    };

}(jQuery, jQuery.fn.dataTable));