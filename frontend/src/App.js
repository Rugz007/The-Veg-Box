import 'antd/dist/antd.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import AdminHome from './components/AdminHome';
import Sales from './containers/Sales';


function App() {
  return (
    <div>
      <Router>
        <Switch>
          {/* <Route exact path='/' component={AdminHome} /> */}
          <Route exact path='/' component={Sales} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;

