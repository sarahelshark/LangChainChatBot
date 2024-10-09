
export async function deleteConversation(uid, modelType,setConversations){

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/delete_conversation?model=${modelType}&uids_to_delete=${uid}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ uids_to_delete: [uid], model_type: modelType }),
      });
      const data = await response.json();


      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete conversation');
      }

      setConversations((prevConversations) => prevConversations.filter(convo => convo.id !== uid));
      alert('Conversation deleted successfully');

    } catch (error) {
      console.error('Error deleting conversation:', error);
      alert(`Failed to delete conversation: ${error.message}`);
    };

};