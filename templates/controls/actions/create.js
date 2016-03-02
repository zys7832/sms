{
    extend: "create",
    editor: editor,
    formButtons: [
         'Create',
         {
             label: 'Continue Add',
             fn: function () {
                this.submit(null,null,null,false )
             }
         }
    ]
}