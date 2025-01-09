function SignIn () {
    return (
        <div>
            <h1>Sign In</h1>
            <form>
                <label className="input-label">
                    Email
                    <input type="email" />
                </label>
                <label className="input-label">
                    Password
                    <input type="password" />
                </label>
                <button>Sign In</button>
            </form>
        </div>
    )
}

export default SignIn;