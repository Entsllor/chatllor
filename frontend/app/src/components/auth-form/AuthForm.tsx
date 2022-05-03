import React, {useState} from "react";
import AuthService from "../../services/auth";

const AuthForm: React.FC = () => {
  const [username, setUsername] = useState<string>("")
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")

  return <div className="AuthForm">
    <input
      className="form-control"
      type="text"
      placeholder="username"
      onChange={event => setUsername(event.target.value)}
    />
    <input
      className="form-control"
      type="text"
      placeholder="email"
      onChange={event => setEmail(event.target.value)}
    />
    <input
      className="form-control"
      type="password"
      placeholder="password"
      onChange={event => setPassword(event.target.value)}
    />
    <button className="btn btn-primary" onClick={e => AuthService.login(username, password)}>
      Login
    </button>
    <button className="btn btn-primary" onClick={e => AuthService.registration(username, email, password)}>
      Registration
    </button>
    <button className="btn btn-danger" onClick={e => AuthService.logout()}>
      Logout
    </button>
  </div>;
};

export default AuthForm
