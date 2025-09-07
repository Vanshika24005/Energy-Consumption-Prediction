import cors from 'cors';
import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';
import authRoutes from './routes/authroute.js';

dotenv.config();
const app = express();
const mangoURI = 'mongodb+srv://bhel:bhel@cluster0.arlfjao.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
app.use(cors());
app.use(express.json());

mongoose.connect(mangoURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'));

  const historySchema = new mongoose.Schema({
    email: String,
    prediction: String,
    timestamp: { type: Date, default: Date.now }
  });
  
  const History = mongoose.model('History', historySchema);
  
  app.get('/api/history', async (req, res) => {
    const { email } = req.query;
    if (!email) return res.status(400).json({ error: 'Email is required' });
  
    try {
      const data = await History.find({ email }).sort({ timestamp: -1 });
      res.json(data);
    } catch (err) {
      res.status(500).json({ error: 'Error fetching history' });
    }
  });
app.use('/api/auth', authRoutes);
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));