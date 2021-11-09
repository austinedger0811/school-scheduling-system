import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid'

import Box from '@mui/material/Box/'
import Typography from '@mui/material/Typography'

const createColumns = (data) => {
  var res = []
  var headers = getHeaders(data, 0)
  for (let i = 0; i < headers.length; i++) {
    res.push({ field: `col${i + 1}`, headerName: headers[i], minWidth: 210})
  }
  return res
}

const getHeaders = (data, i) => {
  var headers = {}
  Object.assign(headers, data[i])
  return Object.keys(headers)
}

const createRows = (data) => {
  var rows = []
  var headers = getHeaders(data, 0)
  for (let i = 0; i < data.length; i++) {
    rows.push(createRow(headers, data[i], i))
  } 
  return rows
}

const createRow = (headers, data, i) => {
  var row = {}
  row.id = (i).toString()
  for (let index = 0; index < headers.length; index++) {
    row[`col${index + 1}`] = data[headers[index]]
  }
  return row
}

const Dashboard = () => {

  const [students, setStudents] = useState([{first_name: '', last_name: ''}])
  const [student, setStudent] = useState(0)
  const [schedule, setSchedule] = useState([])
  const [studentIndex, setStudentIndex] = useState(0)

  useEffect(() => {
    axios.get('http://localhost:5000/api/v1/students')
    .then((response) => {
      setStudents(response.data)
      setStudent(response.data[0]['student_id'])
    })
    .catch(error => console.log(error))
  }, [])

  useEffect(() => {
    axios.get(`http://localhost:5000/api/v1/schedule/${student}`)
    .then((response) => {
      setSchedule(response.data)
    })
    .catch(error => console.log(error))
  }, [student])


  return (
    <>
      <Box mb={4}>
        <Typography mb={2} variant='h5'>
         Student Schedule - {students[studentIndex]['last_name']},  {students[studentIndex]['first_name']}
        </Typography>
        <div style={{ height: 320, width: "100%"}}>
          <DataGrid
            rows={createRows(schedule)}
            columns={createColumns(schedule)}
            hideFooter
          />
        </div>
      </Box>
     <Box mb={4}>
      <Typography mb={2} variant='h5'>Students</Typography>
        <div style={{ height: 600, width: "100%"}}>
          <DataGrid
            rows={createRows(students)}
            columns={createColumns(students)}
            onSelectionModelChange={(index) => {
              setStudentIndex(index)
              setStudent(students[index]['student_id'])
            }}
            
          />
        </div>
      </Box> 
    </>
  )
}

export default Dashboard
