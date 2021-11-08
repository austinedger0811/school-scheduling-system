import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';

import Typography from '@mui/material/Typography'

const createColumns = () => {
  return [
    { field: 'col1', headerName: 'student_id', width: 150 },
    { field: 'col2', headerName: 'first_name', width: 150 }, 
    { field: 'col3', headerName: 'last_name', width: 150 }, 
  ]

}

const createRows = (data) => {
  var rows = []
  for (let i = 0; i < data.length; i++) {
    rows.push(createRow(data, i))
  }
  return rows
}

const createRow = (data, i) => {
  return {id: i + 1, col1: data['student_id'], col2: data['first_name'], col3: data['last_name']} 
}


const Dashboard = () => {

  const [data, setData] = useState([])

  useEffect(() => {
    axios.get('http://localhost:5000/api/v1/students')
    .then((response) => {
      setData(response.data)
    }).catch(error => console.log(error))
  }, [])

  return (
    <div>
      <DataGrid rows={createRows(data)} columns={createColumns()} />
    </div>
  )
}

export default Dashboard
