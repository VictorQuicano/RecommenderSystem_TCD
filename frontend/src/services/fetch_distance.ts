export async function fetchDistance(user1: string, user2: string, distance: string): Promise<number> {
  try {
    const response = await fetch(`http://localhost:5000/compare?u1=${user1}&u2=${user2}&metric=${distance}`);
    const data = await response.json();
    return data
  } catch (error) {
    console.warn("❌ Error al llamar a fetchDistance, devolviendo valor aleatorio:", error);
    return Math.floor(Math.random() * 10) + 1;
  }
}
