console.log("validation")




export const email_validation = (email) =>{
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,150}$/;

    return emailPattern.test(email)
}

//value functions
const add_commas_to_value = (value) =>{

    if(isNaN(value)){
        return 0
    }

    return value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
export const clean_value =(text) =>{

    return text.replace(/\D/g, "");
}

export const value_format = (value_text) =>{
    console.log(value_text)
    if(!value_text){
        return "0.00"
    }

    value_text = String(value_text)

    const cleaned_value = clean_value(value_text);

    if(cleaned_value.length ===0){
        return "0.00";
    }

    let value = Number(cleaned_value);


    let [dollars, cents] = parseFloat(String(value / 100)).toFixed(2).split(".")


    return `${add_commas_to_value(dollars)}.${cents}`

}

export const value_valid = (value) =>{
    const test_value = clean_value(value);

    console.log(test_value)
    const pattern  = /^\d{3,13}$/;

    return pattern.test(test_value);
}

export const clean_email = (email) => {
    const pattern = /[^a-zA-Z0-9._%+\-@]+/g;

    return email.replaceAll(pattern, '')
}

export const name_validation = (name) =>{
    const pattern = /^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-' ][A-Za-zÀ-ÖØ-öø-ÿ]+)?$/;

    return pattern.test(name);
}

export const clean_name = (name) =>{
    const pattern = /[^A-Za-zÀ-ÖØ-öø-ÿ-' ]+/g;

    return name.replaceAll(pattern, '')
}



export const username_validation = (username) =>{
    const pattern = /^[a-zA-Z0-9._-]{3,50}$/;

    return pattern.test(username)
}

export const clean_username = (username) =>{
    const cleanPattern = /[^a-zA-Z0-9._-]+/g;

    return username.replaceAll(cleanPattern, '');
}

export const password_check = (password) =>{
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    return passwordPattern.test(password)
}
