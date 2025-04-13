// src/types.ts
export interface StartMessage {
  type: 'start';
}

export interface AnswerMessage {
  type: 'answer';
  answer: number;
}

export interface ArraysMessage {
  type: 'arrays';
  array1: number[];
  array2: number[];
}

export interface ResultMessage {
  type: 'result';
  message: string;
  correct: boolean;
}

export interface ErrorMessage {
  type: 'error';
  message: string;
}

export type ServerMessage = ArraysMessage | ResultMessage | ErrorMessage;
export type ClientMessage = StartMessage | AnswerMessage;