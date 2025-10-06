import CardDeck from '../components/CardDeck';
import { mockPrimaryDeck, mockSecondaryDeck } from '../data/mockCards';

export default function RecapPage() {
  return (
    <div className="min-h-screen py-8">
      <CardDeck primaryDeck={mockPrimaryDeck} secondaryDeck={mockSecondaryDeck} />
    </div>
  );
}
