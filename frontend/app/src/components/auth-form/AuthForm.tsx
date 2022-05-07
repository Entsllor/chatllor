import React, {useState} from "react";
import AuthService from "../../services/auth";

const AuthForm: React.FC<{ handleAccessToken: CallableFunction }> = (props) => {
  const [username, setUsername] = useState<string>("")
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")

  return <div className="AuthForm">
    <div className="card">
      <div className="card-header">Sign-in</div>
      <div className='card-body'>
        <form onSubmit={event => event.preventDefault()}>
          <input
            className="form-control mb-2"
            type="text"
            placeholder="username"
            onChange={event => setUsername(event.target.value)}
          />
          <input
            className="form-control mb-2"
            type="text"
            placeholder="email"
            onChange={event => setEmail(event.target.value)}
          />
          <input
            className="form-control mb-2"
            type="password"
            placeholder="password"
            onChange={event => setPassword(event.target.value)}
          />
          <div className="d-flex flex-row flex-wrap gap-2 justify-content-end">
            <button className="btn btn-primary" onClick={async () => {
              await AuthService.login(username, password);
              props.handleAccessToken(localStorage.getItem('accessToken'))
            }}>
              Login
            </button>
            <button className="btn btn-primary" onClick={e => AuthService.registration(username, email, password)}>
              Registration
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>;
};

export default AuthForm
