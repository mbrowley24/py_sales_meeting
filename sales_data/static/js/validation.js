console.log("validation")



export const email_validation = (email) =>{
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,150}$/;

    return emailPattern.test(email)


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
