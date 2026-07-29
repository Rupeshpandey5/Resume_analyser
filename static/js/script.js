document.addEventListener(
    "DOMContentLoaded",
    function(){


        const fileInput = document.querySelector(
            "input[type='file']"
        );


        if(fileInput){


            fileInput.addEventListener(
                "change",
                function(){


                    let fileName =
                    this.files[0].name;


                    alert(
                        "Selected Resume: "
                        + fileName
                    );


                }
            );


        }


    }
);