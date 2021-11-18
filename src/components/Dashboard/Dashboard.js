import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { DataGrid } from '@mui/x-data-grid'

import Box from '@mui/material/Box/'
import Button from '@mui/material/Button'
import Fab from '@mui/material/Fab'
import AddIcon from '@mui/icons-material/Add'
import Stack from '@mui/material/Stack'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import InputLabel from '@mui/material/InputLabel'
import FormControl from '@mui/material/FormControl'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'

const BASE_URL = "http://35.237.87.29:8111/api/v1"

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
  const [semesters, setSemesters] = useState([])
  const [semester, setSemester] = useState({})
  const [contacts, setContacts] = useState([])

  useEffect(() => {
    axios.get(`${BASE_URL}/students`)
    .then((response) => {
      setStudents(response.data)
      setStudent(response.data[0]['student_id'])
    })
    .catch(error => console.log(error))
  }, [])

  useEffect(() => {
    axios.post(`${BASE_URL}/schedule/`, {
      semester: semester.semester,
      year: semester.year,
      sid: student
    })
    .then((response) => {
      setSchedule(response.data)
    })
    .catch(error => console.log(error))
  }, [student, semester])

  useEffect(() => {
    axios.get(`${BASE_URL}/semesters`)
    .then((response) => {
      setSemesters(response.data)
      setSemester(response.data[0])
    })
    .catch(error => console.log(error))
  }, [])

  useEffect(() => {
    axios.get(`${BASE_URL}/contacts/${student}`)
    .then((response) => {
      setContacts(response.data)
    })
    .catch(error => console.log(error))
  }, [student])

  const handleChange = (event, child) => {
    setSemester(semesters[child.props.id]);
  };

  const semesterToString = (data) => {
    return `${data.semester} ${data.year}`
  }

  const scheduleSemester = () => {
    axios.post(`${BASE_URL}/schedule_semester`, {
      semester: semester.semester,
      year: semester.year,
      student: student
    }).then((response) => {
      setSchedule(response.data)
    }).catch(error => console.log(error))
  }

  const deleteSchedule = () => {
    axios.post(`${BASE_URL}/clear_schedule`, {
      semester: semester.semester,
      year: semester.year, 
      sid: student
    }).then((response) => {

      setSchedule(response.data)

      axios.get(`${BASE_URL}/semesters`)
      .then((r) => {
        setSemesters(r.data)
        setSemester(r.data[r.data.length - 1])
      })
      .catch(error => console.log(error))

      
      axios.get(`${BASE_URL}/students`)
      .then((r) => {
        setStudents(r.data)
        setStudent(r.data[0]['student_id'])
      })



    }).catch(error => console.log(error))
  }

  const addSemester = () => {
    axios.post(`${BASE_URL}/add_semester`)
    .then((response) => {
      setSemesters(response.data)
      setSemester(response.data[response.data.length - 1])

      axios.get(`${BASE_URL}/students`)
      .then((r) => {
        setStudents(r.data)
        setStudent(r.data[0]['student_id'])
      })
      


    }).catch(error => console.log(error)) 

  }

  return (
    <>
      <Box mb={6}>
        <Stack spacing={4} direction="row">
          <Box>
            <Fab color="primary" aria-label="add" onClick={addSemester}>
              <AddIcon />
            </Fab>
          </Box>
          <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">Semester</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={semesterToString(semester)}
              label="Semester"
              onChange={handleChange}
            >
              {semesters.map((item, id) => <MenuItem id={id} key={id} value={semesterToString(item)}>{semesterToString(item)}</MenuItem>)}
            </Select>
          </FormControl>
          <Button fullWidth variant="contained" onClick={scheduleSemester}>Schedule Students</Button>
          <Button fullWidth variant="contained" color="error" onClick={deleteSchedule}>Delete Semester</Button>
        </Stack>
      </Box>

      <Box sx={{ flexGrow: 1}}>
        <Grid container spacing={6}>
          <Grid item xs={6}>
            <Stack spacing={2} direction="column">

              <Box mb={4}>
                <Typography mb={2} variant='h5'>
                  Schedule - {students[studentIndex]['last_name']},  {students[studentIndex]['first_name']}
                </Typography>
                <div style={{ height: 360, width: "100%"}}>
                  <DataGrid
                    rows={createRows(schedule)}
                    columns={createColumns(schedule)}
                    hideFooter
                  />
                </div>
              </Box>

              <Box mb={4}>
                <Typography mb={2} variant='h5'>
                  Emergency Contacts - {students[studentIndex]['last_name']},  {students[studentIndex]['first_name']}
                </Typography>
                <div style={{ height: 360, width: "100%"}}>
                  <DataGrid
                    rows={createRows(contacts)}
                    columns={createColumns(contacts)}
                    hideFooter
                  />
                </div>
              </Box>
            </Stack>
          </Grid>
  
          <Grid item xs={6}>
            <Box mb={4}>
              <Typography mb={2} variant='h5'>Students</Typography>
                <div style={{ height: 818, width: "100%"}}>
                  <DataGrid
                    hideFooter
                    rows={createRows(students)}
                    columns={createColumns(students)}
                    onSelectionModelChange={(index) => {
                      setStudentIndex(index)
                      setStudent(students[index]['student_id'])
                      setContacts(student)
                    }}
                  />
                </div>
            </Box> 
          </Grid>
        </Grid>
      </Box>
    </>
  )
}

export default Dashboard
