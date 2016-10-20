from voluptuous import Schema, Required, Length

Record = Schema({})
RecordPair = Schema((Record,), Length(2))
TrainingData 

