function SignUp() {
    // we are going to probably use something like clerk and firebase for users and storage.
    return (
        <div>
            <h1>Sign Up</h1>
            <form>
                <label className="input-label">
                    Email
                    <input type="email" />
                </label>
                <label className="input-label">
                    Password
                    <input type="password" />
                </label>
                <label className="input-label">
                    Confirm Password
                    <input type="password" />
                </label>
                <button>Sign Up</button>
            </form>
        </div>
    )
}

export default SignUp;