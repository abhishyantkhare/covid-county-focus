import React from 'react';
import { Grommet } from 'grommet'
import './App.css';
import Main from './components/main/main'
import { Helmet } from "react-helmet";

const TITLE = "COVID-19 County Data"
function App() {
  return (
    <Grommet>
      <Helmet>
        <meta charSet="utf-8" />
        <title>{TITLE}</title>
        <link rel="canonical" href="https://covidcountydata.abhishyant.com" />
      </Helmet>
      <Main />
    </Grommet>
  );
}

export default App;
