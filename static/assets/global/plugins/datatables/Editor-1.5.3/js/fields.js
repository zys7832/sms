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
        },

        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
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
        },
        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('select',conf._input).rules('remove')
                field.disable()
            } else {
                $('select',conf._input).rules("add",conf.rules)
                field.enable()
            }
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
        },
        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('select',conf._input).rules('remove')
                field.disable()
            } else {
                $('select',conf._input).rules("add",conf.rules)
                field.enable()
            }
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
        },
        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
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
'                            <input type="text" id="display" name="' + conf.name +'" readonly="true">' +
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
        },
        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
        }
    };

    _fieldTypes.mdate = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;

            // Create the elements to use for the input
            conf._input = $(
                    '<div>' +
                         '<input class="form-control form-control-inline date-picker" name="'+ conf.name +'" type="text" value="" readonly data-date-format="yyyy-mm-dd"/>'+
                    '</div>')[0];
            conf.mcontrol = $('.date-picker',conf._input)
            conf.mcontrol.datepicker({
                    rtl: Metronic.isRTL(),
                    orientation: "left",
                    autoclose: true
                });
            return conf._input;
        },

        get: function (conf) {
            return $('input', conf._input).attr('value');
        },

        set: function (conf, val) {
            val = val.split(" ")[0]
            conf.mcontrol.datepicker('setDate',val)
            $('input', conf._input).attr('value', val);
        },

        enable: function (conf) {
            conf._enabled = true;
            $('input',conf._input).attr('disabled',false);
        },

        disable: function (conf) {
            conf._enabled = false;
            $('input',conf._input).attr('disabled',true);
        },

        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
        }
    };

    _fieldTypes.mdatetime = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;

            // Create the elements to use for the input
            conf._input = $(
                    '<div>' +
                         '<input class="form-control form-control-inline date-picker format_datetime" name="'+ conf.name +'" type="text" value="" readonly data-date-format="yyyy-mm-dd"/>'+
                    '</div>')[0];
            conf.mcontrol = $('.format_datetime',conf._input)

            conf.mcontrol.datetimepicker({
                autoclose: true,
                isRTL: Metronic.isRTL(),
                format : 'yyyy-mm-dd hh:ii:ss',
                pickerPosition: (Metronic.isRTL() ? "bottom-right" : "bottom-left")
            });
            return conf._input;
        },

        get: function (conf) {
            return $('input', conf._input).attr('value');
        },

        set: function (conf, val) {
            val = val.split('+')[0]
            $('input', conf._input).attr('value', val);
            conf.mcontrol.datetimepicker('update')
        },

        enable: function (conf) {
            conf._enabled = true;
            $('input',conf._input).attr('disabled',false);
        },

        disable: function (conf) {
            conf._enabled = false;
            $('input',conf._input).attr('disabled',true);
        },

        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
        }
    };

    _fieldTypes.treeselect1 = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;


            var $div =
                $('<div>' +
                    '<div class="input-group col-md-12">'+
                        '<input id="tree_input" name="' + conf.name +'" class="form-control" type="text" placeholder="" readonly>' +
                        '<span class="input-group-btn">'+
                            '<button class="btn default date-reset" type="button"><i class="fa fa-times"></i></button>'+
                        '</span>'+
                    '</div>' +
                    '<div id="tree" style="display:block;position:absolute;border:1px solid grey;height:200px;width:500px;overflow:auto;background-color:white">' +
                    '<div id="tree_content" class="tree-demo"></div>' +
                    '</div>'+
                '</div>')

            $div.find("#tree_content").jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    },
                    // so that create works
                    "check_callback": true,
                    'data': conf.items
                },
                "types": {
                    "default": {
                        "icon": "fa fa-folder icon-state-warning icon-lg"
                    },
                    "file": {
                        "icon": "fa fa-file icon-state-warning icon-lg"
                    }
                },
                "state": { "key": "demo2" },
                "plugins": [ "contextmenu", "dnd", "state", "types" ]
            }).on('select_node.jstree', function (e, data) {
                $div.find("#tree_input").val(data.node.text)
                $div.find("#tree").hide()
            })

            $div.find(".date-reset").click(function(event){
                $div.find("#tree_content").jstree("deselect_all")
                $div.find("#tree_input").val("")
            })

            $div.find("#tree_input").click(function (event) {
                var
                        $tree_input = $(this),
                        $tree = $("#tree",$div),
                        $tree_input_offset = $tree_input.offset(),
                        $group = $div,
                        $group_offset = $group.offset(),
                        tree_left = $tree_input.offset().left - $group_offset.left + 15

                $tree.toggle().css("zIndex", 20000)
                $tree.css({
                    left: tree_left + 'px',
                    width: $tree_input.css('width')
                })
                return false
            })
            $("#tree",$div).click(function (event) {
                return false
            })
            $("body").click(function (event) {
                $('#tree',$div).hide()
            })
            conf._input = $div
            return conf._input;
        },

        get: function (conf) {
            var $jstree = $("#tree_content",conf._input),
            result =  $jstree.jstree("get_selected")

            if (result.length>0){
                return result[0]
            } else {
                return ''
            }
        },

        set: function (conf, val) {
            var $jstree = $("#tree_content",conf._input)
            setTimeout(function(){
                $('#tree_input',conf._input).val('')
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
        },
        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
        }
    };

    _fieldTypes.ajaxtreeselect = {
        create: function (conf) {
            var that = this;

            conf._enabled = true;


            var $div =
                $('<div>' +
                    '<div class="input-group col-md-12">'+
                        '<input id="tree_input" name="' + conf.name.replace('.','_') +'" class="form-control" type="text" placeholder="" readonly>' +
                        '<span class="input-group-btn">'+
                            '<button class="btn default date-reset" type="button"><i class="fa fa-times"></i></button>'+
                        '</span>'+
                    '</div>' +
                    '<div id="tree" style="display:block;position:absolute;border:1px solid grey;height:200px;width:500px;overflow:auto;background-color:white">' +
                    '<div id="tree_content'+ conf.name.replace('.','_') +'" class="tree-demo"></div>' +
                    '</div>'+
                '</div>')

            $div.find("#tree_content" + conf.name.replace('.','_')).jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    },
                    // so that create works
                    "check_callback": true,
                    'data': {
                        'url' : function (node) {
                          return conf.ajax_url;
                        },
                        'type':'post',
                        'data' : function (node) {
                          return { 'parent' : node.id,'level':node.parents.length };
                        }
                    }
                }}).on('select_node.jstree', function (e, data) {
                $div.find("#tree_input").val(data.node.text)
                $div.find("#tree").hide()
            })

            $div.find(".date-reset").click(function(event){
                $div.find("#tree_content"+conf.name.replace('.','_')).jstree("deselect_all")
                $div.find("#tree_input").val("")
            })

            $div.find("#tree_input").click(function (event) {
                var
                        $tree_input = $(this),
                        $tree = $("#tree",$div),
                        $tree_input_offset = $tree_input.offset(),
                        $group = $div,
                        $group_offset = $group.offset(),
                        tree_left = $tree_input.offset().left - $group_offset.left + 15

                $tree.toggle().css("zIndex", 20000)
                $tree.css({
                    left: tree_left + 'px',
                    width: $tree_input.css('width')
                })
                return false
            })
            $("#tree",$div).click(function (event) {
                return false
            })
            $("body").click(function (event) {
                $('#tree',$div).hide()
            })
            conf._input = $div
            return conf._input;
        },

        get: function (conf) {
            var $jstree = $("#tree_content"+conf.name.replace('.','_'),conf._input),
            result =  $jstree.jstree("get_selected")

            if (result.length>0){
                return result[0]
            } else {
                return conf.default_val
            }
        },

        set: function (conf, val) {
            conf.default_val = val
            var $jstree = $("#tree_content" + conf.name.replace('.','_'),conf._input)
            setTimeout(function(){
                $('#tree_input',conf._input).val('')
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
        },
        rules : function(conf,action){
            field = this.field(conf.name)
            if(action==='edit' && !conf.editable){
                $('input',conf._input).rules('remove')
                field.disable()
            } else {
                $('input',conf._input).rules("add",conf.rules)
                field.enable()
            }
        }
    };

}(jQuery, jQuery.fn.dataTable));