import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  ListItemSecondaryAction,
  IconButton, 
  Chip, 
  Paper, 
  Divider,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent
} from '@mui/material';
import { 
  CheckCircle, 
  RadioButtonUnchecked, 
  Delete, 
  Edit,
  CalendarToday,
  Flag
} from '@mui/icons-material';
import { format } from 'date-fns';
import { getTasks, markTaskCompleted, markTaskPending, deleteTask, Task } from '../services/api';
import { useNavigate } from 'react-router-dom';

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<string>('all');
  const navigate = useNavigate();

  const fetchTasks = async () => {
    try {
      let fetchedTasks;
      if (filter === 'completed') {
        fetchedTasks = await getTasks(true);
      } else if (filter === 'pending') {
        fetchedTasks = await getTasks(false);
      } else {
        fetchedTasks = await getTasks();
      }
      setTasks(fetchedTasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [filter]);

  const handleFilterChange = (event: SelectChangeEvent) => {
    setFilter(event.target.value);
  };

  const handleToggleComplete = async (task: Task) => {
    try {
      if (task.completed) {
        await markTaskPending(task.id);
      } else {
        await markTaskCompleted(task.id);
      }
      fetchTasks();
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await deleteTask(id);
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleEditTask = (id: number) => {
    navigate(`/edit-task/${id}`);
  };

  const getPriorityColor = (priority: string | null) => {
    switch (priority) {
      case 'High':
        return 'error';
      case 'Medium':
        return 'warning';
      case 'Low':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Task Manager
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={() => navigate('/add-task')}
        >
          Add New Task
        </Button>
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel id="filter-label">Filter</InputLabel>
          <Select
            labelId="filter-label"
            value={filter}
            label="Filter"
            onChange={handleFilterChange}
          >
            <MenuItem value="all">All Tasks</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Paper elevation={2}>
        <List>
          {tasks.length === 0 ? (
            <ListItem>
              <ListItemText primary="No tasks found" />
            </ListItem>
          ) : (
            tasks.map((task, index) => (
              <React.Fragment key={task.id}>
                {index > 0 && <Divider />}
                <ListItem 
                  sx={{ 
                    bgcolor: task.completed ? 'rgba(0, 0, 0, 0.04)' : 'inherit',
                    '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.08)' }
                  }}
                >
                  <ListItemIcon onClick={() => handleToggleComplete(task)} sx={{ cursor: 'pointer' }}>
                    {task.completed ? 
                      <CheckCircle color="success" /> : 
                      <RadioButtonUnchecked />
                    }
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography 
                        variant="subtitle1" 
                        sx={{ 
                          textDecoration: task.completed ? 'line-through' : 'none',
                          color: task.completed ? 'text.secondary' : 'text.primary'
                        }}
                      >
                        {task.title}
                      </Typography>
                    }
                    secondary={
                      <Box sx={{ mt: 1 }}>
                        {task.description && (
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            {task.description}
                          </Typography>
                        )}
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          {task.due_date && (
                            <Chip 
                              size="small" 
                              icon={<CalendarToday fontSize="small" />} 
                              label={format(new Date(task.due_date), 'MMM d, yyyy')} 
                              variant="outlined" 
                            />
                          )}
                          {task.priority && (
                            <Chip 
                              size="small" 
                              icon={<Flag fontSize="small" />} 
                              label={task.priority} 
                              color={getPriorityColor(task.priority) as any}
                              variant="outlined" 
                            />
                          )}
                        </Box>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end" onClick={() => handleEditTask(task.id)}>
                      <Edit />
                    </IconButton>
                    <IconButton edge="end" onClick={() => handleDeleteTask(task.id)}>
                      <Delete />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              </React.Fragment>
            ))
          )}
        </List>
      </Paper>
    </Box>
  );
};

export default TaskList;
