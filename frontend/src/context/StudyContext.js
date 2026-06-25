import { createContext, useState } from "react";

export const StudyContext = createContext();

export const StudyProvider = ({ children }) => {
  const [selectedChapter, setSelectedChapter] = useState("");
  const [currentNote, setCurrentNote] = useState(null);

  return (
    <StudyContext.Provider
      value={{
        selectedChapter,
        setSelectedChapter,
        currentNote,
        setCurrentNote,
      }}
    >
      {children}
    </StudyContext.Provider>
  );
};