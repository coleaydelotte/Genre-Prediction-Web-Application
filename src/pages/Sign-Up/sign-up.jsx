function SignUp() {
    return (
      <div className="signup-container">
        <div className="signup-card">
          <h1 className="signup-title">Create Account</h1>
          <form className="signup-form">
            <label className="input-label">
              Email
              <input type="email" placeholder="you@example.com" />
            </label>
            <label className="input-label">
              Password
              <input type="password" placeholder="••••••••" />
            </label>
            <label className="input-label">
              Confirm Password
              <input type="password" placeholder="••••••••" />
            </label>
            <button type="submit" className="signup-btn">Sign Up</button>
          </form>
          <p className="signup-footer">
            Already have an account? <a href="/login">Log in</a>
          </p>
        </div>
      </div>
    );
  }
  
  export default SignUp;
  