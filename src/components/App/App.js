import React from 'react'

import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'

import Navbar from '../Navbar/Navbar'
import Dashboard from '../Dashboard/Dashboard'

const App = () => {

  return (
    <React.Fragment>
      <Navbar />
      <Container maxWidth="xl">
        <Dashboard />
      </Container>
    </React.Fragment>
  );
}

export default App;
