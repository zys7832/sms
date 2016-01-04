{
    extend: "print",
    text: 'print',
    autoPrint: false,
    customize: function ( win ) {
                $(win.document.body)
                        .css({'font-size':'10pt','background-color':'white'})

                $(win.document.body).find( 'table' )
                    .addClass( 'compact' )
                    .css( 'font-size', 'inherit' );

                    $(win.document.body).find("h1").html('')
    }
}